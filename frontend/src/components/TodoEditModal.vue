<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Edit Task</h2>
        <button @click="close" class="btn-close">✕</button>
      </div>
      <form @submit.prevent="save" class="modal-form">
        <div class="form-group">
          <label for="edit-title">Title *</label>
          <input
            id="edit-title"
            v-model="editForm.title"
            type="text"
            required
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="edit-description">Description</label>
          <textarea
            id="edit-description"
            v-model="editForm.description"
            class="form-textarea"
            rows="3"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="edit-priority">Priority</label>
          <select v-model="editForm.priority" id="edit-priority" class="form-select">
            <option value="1">Low</option>
            <option value="2">Medium</option>
            <option value="3">High</option>
          </select>
        </div>
        <div class="form-group">
          <label for="edit-status">Status</label>
          <select v-model="editForm.status" id="edit-status" class="form-select">
            <option value="pending">Pending</option>
            <option value="in_progress">In Progress</option>
            <option value="blocked">Blocked</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        <div class="modal-actions">
          <button type="submit" class="btn btn-primary">
            Save Changes
          </button>
          <button type="button" @click="close" class="btn btn-secondary">
            Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  name: 'TodoEditModal',
  props: {
    todo: {
      type: Object,
      required: true
    }
  },
  emits: ['save', 'close'],
  setup(props, { emit }) {
    const editForm = ref({
      title: '',
      description: '',
      priority: '3',
      status: 'pending'
    })

    watch(
      () => props.todo,
      (newTodo) => {
        editForm.value = {
          title: newTodo.title || '',
          description: newTodo.description || '',
          priority: newTodo.priority || 1,
          status: newTodo.status || 1
        }
      },
      { immediate: true }
    )

    const save = () => {
      emit('save', editForm.value)
    }

    const close = () => {
      emit('close')
    }

    return {
      editForm,
      save,
      close
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  transition: color 0.3s;
}

.btn-close:hover {
  color: #333;
}

.modal-form {
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  font-size: 0.95rem;
  transition: border-color 0.3s;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-textarea {
  resize: vertical;
}

.modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.btn {
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: blue;
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
  background: white;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}
</style>
