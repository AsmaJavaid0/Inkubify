export interface ToastMessage {
  id: number
  type: 'success' | 'error' | 'info' | 'warning'
  text: string
}

const toasts = ref<ToastMessage[]>([])
let nextId = 1

export function useToast() {
  function push(text: string, type: ToastMessage['type'] = 'info', durationMs = 4500) {
    const id = nextId++
    toasts.value.push({ id, type, text })
    if (import.meta.client && durationMs > 0) {
      setTimeout(() => remove(id), durationMs)
    }
  }

  function remove(id: number) {
    toasts.value = toasts.value.filter((t: ToastMessage) => t.id !== id)
  }

  return {
    toasts: readonly(toasts),
    success: (text: string) => push(text, 'success'),
    error: (text: string) => push(text, 'error', 6000),
    info: (text: string) => push(text, 'info'),
    warning: (text: string) => push(text, 'warning'),
    remove,
  }
}
