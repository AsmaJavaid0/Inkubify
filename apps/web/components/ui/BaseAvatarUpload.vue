<script setup lang="ts">
import { Camera, Trash2 } from 'lucide-vue-next'

interface Props {
  modelValue: string | null | undefined
  fullName?: string
  userId?: string
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  fullName: 'Founder',
  userId: '',
  disabled: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: string | null]
}>()

const supabase = useSupabaseClient()
const toast = useToast()

const fileInputRef = ref<HTMLInputElement | null>(null)
const uploading = ref(false)
const localError = ref('')

const initials = computed(() => {
  const parts = (props.fullName || 'F').trim().split(/\s+/)
  if (parts.length >= 2) {
    return `${parts[0]![0] ?? ''}${parts[1]![0] ?? ''}`.toUpperCase()
  }
  return (parts[0]?.slice(0, 2) || 'F').toUpperCase()
})

const ALLOWED_TYPES = new Set(['image/jpeg', 'image/png', 'image/webp'])
const MAX_BYTES = 2 * 1024 * 1024 // 2 MB

async function cropSquareBlob(file: File): Promise<{ blob: Blob; ext: string; mime: string }> {
  const mime = file.type === 'image/png' ? 'image/png' : file.type === 'image/webp' ? 'image/webp' : 'image/jpeg'
  const ext = mime === 'image/png' ? 'png' : mime === 'image/webp' ? 'webp' : 'jpg'

  const bitmap = await createImageBitmap(file)
  const size = Math.min(bitmap.width, bitmap.height)
  const target = Math.min(512, size)
  const sx = (bitmap.width - size) / 2
  const sy = (bitmap.height - size) / 2

  const canvas = document.createElement('canvas')
  canvas.width = target
  canvas.height = target
  const ctx = canvas.getContext('2d')
  if (!ctx) throw new Error('Canvas unavailable')
  ctx.drawImage(bitmap, sx, sy, size, size, 0, 0, target, target)
  bitmap.close()

  const blob = await new Promise<Blob | null>((resolve) =>
    canvas.toBlob(resolve, mime, 0.9),
  )
  if (!blob) throw new Error('Failed to process image')
  return { blob, ext, mime }
}

async function handleFileSelect(event: Event) {
  localError.value = ''
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ''
  if (!file) return

  if (!ALLOWED_TYPES.has(file.type)) {
    localError.value = 'Please choose a JPG, PNG, or WebP image.'
    return
  }
  if (file.size > MAX_BYTES) {
    localError.value = 'Image must be 2 MB or smaller.'
    return
  }
  if (!props.userId) {
    localError.value = 'Unable to upload photo before user session is ready.'
    return
  }

  uploading.value = true
  try {
    const { blob, ext, mime } = await cropSquareBlob(file)
    const path = `${props.userId}/avatar.${ext}`
    const { error } = await supabase.storage.from('avatars').upload(path, blob, {
      contentType: mime,
      upsert: true,
    })
    if (error) {
      throw error
    }
    const { data: publicUrlData } = supabase.storage.from('avatars').getPublicUrl(path)
    const cacheBustedUrl = `${publicUrlData.publicUrl}?t=${Date.now()}`
    emit('update:modelValue', cacheBustedUrl)
    toast.success('Profile photo updated')
  } catch (err: unknown) {
    localError.value =
      err instanceof Error ? err.message : 'Could not upload photo. Please try again.'
  } finally {
    uploading.value = false
  }
}

function removePhoto() {
  emit('update:modelValue', null)
}
</script>

<template>
  <div class="space-y-2">
    <div class="flex items-center gap-4">
      <div
        class="relative flex h-20 w-20 shrink-0 items-center justify-center overflow-hidden rounded-card border border-navy-border bg-navy-700 text-lg font-bold text-gold-500"
      >
        <img
          v-if="props.modelValue"
          :src="props.modelValue"
          :alt="`${props.fullName} profile photo`"
          class="h-full w-full object-cover"
        >
        <span v-else>{{ initials }}</span>
      </div>

      <div class="space-y-2">
        <div class="flex flex-wrap items-center gap-2">
          <input
            ref="fileInputRef"
            type="file"
            accept="image/jpeg,image/png,image/webp"
            class="sr-only"
            :disabled="props.disabled || uploading"
            @change="handleFileSelect"
          >
          <button
            type="button"
            :disabled="props.disabled || uploading"
            class="inline-flex items-center gap-2 rounded-btn border border-snow-100/20 bg-navy-700 px-3.5 py-2 text-xs font-medium text-snow-100 hover:border-snow-100/40 disabled:opacity-50"
            @click="fileInputRef?.click()"
          >
            <Camera class="h-4 w-4 text-gold-500" aria-hidden="true" />
            <span>{{ uploading ? 'Uploading...' : props.modelValue ? 'Change photo' : 'Upload photo' }}</span>
          </button>

          <button
            v-if="props.modelValue"
            type="button"
            :disabled="props.disabled || uploading"
            class="inline-flex items-center gap-1.5 rounded-btn px-2.5 py-2 text-xs font-medium text-snow-muted hover:text-danger"
            @click="removePhoto"
          >
            <Trash2 class="h-3.5 w-3.5" aria-hidden="true" />
            <span>Remove</span>
          </button>
        </div>
        <p class="text-xs text-snow-muted">
          Optional. JPG, PNG or WebP up to 2 MB (auto-cropped square).
        </p>
      </div>
    </div>

    <p v-if="localError" role="alert" class="text-xs font-medium text-danger">
      {{ localError }}
    </p>
  </div>
</template>
