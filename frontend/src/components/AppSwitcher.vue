<template>
  <Popover
    placement="right-start"
    class="flex w-full"
  >
    <template #target="{ togglePopover }">
      <button
        :class="[
          active ? 'bg-surface-gray-2' : 'text-ink-gray-8',
          'group w-full flex h-7 items-center justify-between rounded px-2 text-base hover:bg-surface-gray-2',
        ]"
        @click.prevent="togglePopover()"
      >
        <div class="flex gap-2">
          <AppsIcon class="size-4" />
          <span class="whitespace-nowrap"> Apps </span>
        </div>
        <LucideChevronRight class="size-4 text-ink-gray-6" />
      </button>
    </template>
    <template #body>
      <div
        class="grid grid-cols-3 justify-between mx-3 p-2 rounded-lg border border-gray-100 bg-surface-white shadow-xl"
      >
        <div
          v-for="app in apps.data"
          :key="app.name"
        >
          <a
            :href="app.route"
            class="flex flex-col gap-1.5 rounded justify-center items-center py-2 px-1 hover:bg-surface-gray-2"
          >
            <img
              class="size-8"
              :src="app.logo"
            />
            <div
              class="text-sm text-ink-gray-7"
              @click="app.onClick"
            >
              {{ app.title }}
            </div>
          </a>
        </div>
      </div>
    </template>
  </Popover>
</template>
<script setup>
import AppsIcon from "@/components/AppsIcon.vue"
import { Popover, createResource } from "frappe-ui"

const props = defineProps({
  active: Boolean,
})

const apps = createResource({
  url: "frappe.apps.get_apps",
  cache: "apps",
  auto: true,
  transform: (data) => {
    let apps = [
      {
        name: "frappe",
        logo: "/assets/frappe/images/framework.png",
        title: "Desk",
        route: "/app",
      },
    ]
    data.map((app) => {
      if (app.name === "dms") return
      apps.push({
        name: app.name,
        logo: app.logo,
        title: app.title,
        route: app.route,
      })
    })

    return apps
  },
})
</script>
