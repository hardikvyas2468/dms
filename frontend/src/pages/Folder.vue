<template>
  <GenericPage
    :verify="currentFolder"
    :get-entities="getFolderContents"
    :icon="LucideFolderClosed"
    :primary-message="'Folder is Empty'"
  />
</template>

<script setup>
import GenericPage from "@/components/GenericPage.vue"
import { inject, onMounted, onBeforeUnmount, watch, computed } from "vue"
import { useStore } from "vuex"
import { createResource } from "frappe-ui"
import { COMMON_OPTIONS } from "@/resources/files"
import { setBreadCrumbs, prettyData, setCache } from "@/utils/files"
import router from "@/router"
import { LucideFolderClosed } from "lucide-vue-next"

const store = useStore()
const realtime = inject("realtime")
const emitter = inject("emitter")

const props = defineProps({
  entityName: String,
  team: String,
})

const getFolderContents = createResource({
  ...COMMON_OPTIONS,
  url: "dms.api.list.files",
  makeParams: (params) => ({
    ...params,
    // Disable all checks, return all children
    personal: -2,
    entity_name: props.entityName,
    team: props.team,
  }),
  cache: ["folder", props.entityName],
})
setCache(getFolderContents, ["folder", props.entityName])

onMounted(() => {
  realtime.doc_subscribe("DMS File", props.entityName)
  realtime.doc_open("DMS File", props.entityName)
  realtime.on("doc_viewers", (data) => {
    store.state.connectedUsers = data.users
    userInfo.submit({ users: JSON.stringify(data.users) })
  })
})

onBeforeUnmount(() => {
  realtime.off("doc_viewers")
  store.state.connectedUsers = []
  realtime.doc_close("DMS File", currentFolder.data?.name)
  realtime.doc_unsubscribe("DMS File", currentFolder.data?.name)
})

const onSuccess = (entity) => {
  if (router.currentRoute.value.params.entityName !== entity.name) return
  document.title = "Folder - " + entity.title
  setBreadCrumbs(entity.breadcrumbs, entity.is_private, () =>
    emitter.emit("rename")
  )
}

const e = computed(() => props.entityName)
let currentFolder = createResource({
  url: "dms.api.permissions.get_entity_with_permissions",
  makeParams: (e) => ({ entity_name: e }),
  transform(entity) {
    return prettyData([entity])[0]
  },
  onSuccess,
  onError() {
    if (!store.getters.isLoggedIn) router.push({ name: "Login" })
  },
})
watch(e, (v) => currentFolder.fetch(v), { immediate: true })

let userInfo = createResource({
  url: "frappe.desk.form.load.get_user_info_for_viewers",
  onSuccess(data) {
    data = Object.values(data)
    data.forEach((item) => {
      // compatibility with document awareness
      if (item.fullname) {
        item.avatar = item.image
        item.name = item.fullname
        delete item.image
        delete item.fullname
      }
    })
    store.state.connectedUsers = data
  },
})
</script>
