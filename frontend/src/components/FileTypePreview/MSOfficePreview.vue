<template>
  <iframe
    v-if="warned && jwt_token"
    :src="'https://view.officeapps.live.com/op/embed.aspx?src=' + srcUrl"
    class="w-[80%] mx-auto h-[90%]"
    frameborder="0"
  >
    This is an embedded Microsoft Office document, powered by Office
    Online>.</iframe
  >
  <div
    v-else
    class="max-w-[350px] p-8 z-10 bg-surface-white rounded-md text-neutral-100 text-xl text-center font-medium shadow-xl flex flex-col justify-center items-center"
  >
    <div
      v-if="error"
      class="text-base"
    >
      <LucideSettings class="size-8 mb-6 mx-auto" />
      Please ask your site's administrator to set the access key in the
      <a
        href="/app/dms-site-settings"
        class="underline"
        >Settings</a
      >.
    </div>
    <template v-else>
      <LucideAlertCircle class="size-8 mb-6" />
      <span class="mb-4">Are you sure you want to preview?</span>
      <span class="text-base text-center text-ink-gray-7">
        This preview is generated by an external service (<b>Microsoft</b>), not
        by DMS. For extra privacy, we'd suggest downloading.
      </span>
      <Button
        class="mt-4 w-full"
        variant="subtle"
        :loading="jwt_token === ''"
        @click="warned = true"
      >
        View anyway
      </Button>
      <Button
        class="mt-4 w-full"
        variant="solid"
        @click="download"
      >
        Download
      </Button>
    </template>
  </div>
</template>
<script setup>
import { computed, ref, watch } from "vue"
const props = defineProps({
  previewEntity: Object,
})

const warned = ref(false)
watch(warned, async () => {
  jwt_token.value = ""
  const res = await fetch(
    "/api/method/dms.api.files.create_auth_token?entity_name=" +
      props.previewEntity.name
  )
  const { message } = JSON.parse(await res.text())
  if (message) {
    jwt_token.value = message
  } else {
    error.value = "Please set up your DMS Settings."
  }
})

const jwt_token = ref(null)
const error = ref(null)
const srcUrl = computed(() =>
  encodeURIComponent(
    new URL(
      `/api/method/dms.api.files.get_file_content?jwt_token=${jwt_token.value}&entity_name=${props.previewEntity.name}&trigger_download=1`,
      window.location.origin
    ).href
  )
)
const download = () => (window.location.ref = srcUrl.value)
</script>
