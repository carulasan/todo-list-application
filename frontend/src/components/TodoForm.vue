<template>
  <form @submit.prevent="handleSubmit" class="todo-form">
    <div class="form-group">
      <label for="title">Task Title *</label>
      <input
        id="title"
        v-model="form.title"
        type="text"
        placeholder="Enter your task..."
        required
        class="form-input"
      />
    </div>

    <div class="form-group">
      <label for="description">Description</label>
      <textarea
        id="description"
        v-model="form.description"
        placeholder="Add task details (optional)"
        class="form-textarea"
        rows="3"
      ></textarea>
    </div>

    <div class="form-group">
      <label for="priority">Priority</label>
      <select v-model="form.priority" id="priority" class="form-select">
        <option value="3">Low</option>
        <option value="2">Medium</option>
        <option value="1">High</option>
      </select>
    </div>
    <div>
      <label for="tags" class="mb-4">Tags</label>
      <div class="mb-4" />
      <button
        rows="3"
        @click.prevent="handleAddTags(item)"
        class="form-input btn-seconday"
        v-for="item in tags"
        :key="item"
      >
        <span
          v-if="form"
          :style="{ color: form.tags.includes(item) ? 'green' : 'grey' }"
        >
          {{ item }}</span
        >
      </button>
    </div>

    <button type="submit" class="btn btn-primary mt-5" :disabled="loading">
      {{ loading ? "Creating..." : "Add Todo" }}
    </button>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </form>
</template>

<script>
import { ref } from "vue";
import todoService from "../api/todoService";
import Datepicker from "vue3-datepicker";
export default {
  components: {
    Datepicker,
  },
  name: "TodoForm",
  emits: ["todo-created"],
  setup(props, { emit }) {
    const form = ref({
      title: "",
      description: "",
      priority: 1,
      tags: [],
    });
    const loading = ref(false);
    const error = ref(null);
    const tags = ref(["Technology", "Cooking", "Marketing", "Construction", "Music"]);

    const handleAddTags = (tag) => {
      if (!tag) return;

      const tags = form.value.tags; // access ref array

      const index = tags.indexOf(tag);
      if (index !== -1) {
        // Tag exists → remove it
        tags.splice(index, 1);
      } else {
        // Tag doesn't exist → add it
        tags.push(tag);
      }
    };

    const handleSubmit = async () => {
      if (!form.value.title.trim()) {
        error.value = "Title is required";
        return;
      }

      loading.value = true;
      error.value = null;

      try {
        await todoService.createTodo({
          title: form.value.title,
          description: form.value.description,
          priority: form.value.priority,
          tags: form.value.tags,
        });

        form.value = {
          title: "",
          description: "",
          priority: "3",
          tags: []
        };

        emit("todo-created");
      } catch (err) {
        console.error("Error creating todo:", err);
        error.value = err.response?.data?.detail || "Failed to create todo";
      } finally {
        loading.value = false;
      }
    };

    return {
      tags,
      form,
      loading,
      error,
      handleSubmit,
      handleAddTags,
    };
  },
};
</script>

<style scoped>
.todo-form {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
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
  transition:
    border-color 0.3s,
    box-shadow 0.3s;
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

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  width: 100%;
}

.btn-primary {
  background: blue;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.mt-5{
  margin-top: 5px;
}

.error-message {
  color: #e74c3c;
  margin-top: 10px;
  font-size: 0.9rem;
  padding: 8px 12px;
  background: #fadbd8;
  border-radius: 4px;
}

.btn-seconday {
  cursor: pointer;
}
.btn-delete:hover {
  background: #e74c3c;
  transform: scale(1.1);
}
.mb-4 {
  margin-bottom: 4px;
}
</style>
