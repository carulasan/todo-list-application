<template>
  <div class="todo-list-container">
    <div v-if="todos.length === 0" class="empty-state">
      <p class="empty-message">No tasks yet. Create one to get started!</p>
    </div>

    <div v-else class="todo-stats">
      <div class="stat">
        <span class="stat-label">Todos:</span>
        <span class="stat-value">{{ todos.length }}</span>
      </div>
      <div class="stat">
        <span class="stat-label">Pending:</span>
        <span class="stat-value todo">{{ pendingCount }}</span>
      </div>
      <div class="stat">
        <span class="stat-label">Blocked:</span>
        <span class="stat-value blocked">{{ blockedCount }}</span>
      </div>
      <div class="stat">
        <span class="stat-label">In Progres:</span>
        <span class="stat-value inprogress">{{ inProgressCount }}</span>
      </div>

      <div class="stat">
        <span class="stat-label">Completed:</span>
        <span class="stat-value completed">{{ completedCount }}</span>
      </div>
    </div>

    <ul class="todo-list">
      <li
        v-for="todo in sortedTodos"
        :key="todo.id"
        class="todo-item"
        :class="{ completed: todo.status === 'completed' }"
      >
        <div class="todo-content">
          <div class="todo-header">
            <input
              type="checkbox"
              :checked="todo.status === 'completed'"
              @change="toggleTodo(todo)"
              class="todo-checkbox"
            />
            <h3 class="todo-title">{{ todo.title }}</h3>
            <span
              v-if="todo.priority"
              class="todo-priority"
              :class="`priority-${todo.priority}`"
            >
              Priority: {{ todo.priority }}
            </span>
          </div>
          <p v-if="todo.description" class="todo-description">
            {{ todo.description }}
          </p>
          <div v-if="todo.tags" class="tags">
            Tags:
            <span v-for="tag in todo.tags" :key="tag" class="todo-tag">
              {{ tag }},
            </span>
          </div>
        </div>
        <div class="todo-actions">
          <button
            @click="editTodo(todo)"
            class="btn-icon btn-edit"
            title="Edit"
          >
            Edit
          </button>
          <button @click="deleteTodo(todo.id)" class="btn-icon btn-delete">
            Delete
          </button>
        </div>

        <TodoEditModal
          v-if="editingTodo && editingTodo.id === todo.id"
          :todo="editingTodo"
          @save="handleSave"
          @close="editingTodo = null"
        />
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, computed } from "vue";
import todoService from "../api/todoService";
import TodoEditModal from "./TodoEditModal.vue";

export default {
  name: "TodoList",
  components: {
    TodoEditModal,
  },
  props: {
    todos: {
      type: Array,
      default: () => [],
    },
  },
  emits: ["todo-updated", "todo-deleted"],
  setup(props, { emit }) {
    const editingTodo = ref(null);
    const loading = ref(false);
    const sortedTodos = computed(() => {
      return [...props.todos].sort((a, b) => {
        const priorityOrder = { high: 1, medium: 2, low: 3 };
        return (
          (priorityOrder[a.priority] || 2) - (priorityOrder[b.priority] || 2)
        );
      });
    });

    const completedCount = computed(() => {
      return props.todos.filter((todo) => todo.status === "completed").length;
    });

    const pendingCount = computed(() => {
      return props.todos.filter((todo) => todo.status === "pending").length;
    });

    const blockedCount = computed(() => {
      return props.todos.filter((todo) => todo.status === "blocked").length;
    });

    const inProgressCount = computed(() => {
      return props.todos.filter((todo) => todo.status === "in_progress").length;
    });

    const toggleTodo = async (todo) => {
      const newStatus = todo.status === "completed" ? "todo" : "completed";
      try {
        await todoService.updateTodo(todo.id, { status: newStatus });
        emit("todo-updated");
      } catch (err) {
        console.error("Error updating todo:", err);
      }
    };

    const editTodo = (todo) => {
      editingTodo.value = { ...todo };
    };

    const handleSave = async (updatedData) => {
      try {
        const payload = {
          ...updatedData,
        };

        await todoService.updateTodo(editingTodo.value.id, payload);
        editingTodo.value = null;
        emit("todo-updated");
      } catch (err) {
        console.error("Error saving todo:", err);
      }
    };

    const deleteTodo = async (todoId) => {
      if (confirm("Are you sure you want to delete this todo?")) {
        try {
          await todoService.deleteTodo(todoId);
          emit("todo-deleted");
        } catch (err) {
          console.error("Error deleting todo:", err);
        }
      }
    };

    return {
      editingTodo,
      sortedTodos,
      completedCount,
      blockedCount,
      pendingCount,
      inProgressCount,
      toggleTodo,
      editTodo,
      handleSave,
      deleteTodo,
      loading,
    };
  },
};
</script>

<style scoped>
.todo-list-container {
  width: 100%;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.empty-message {
  font-size: 1.1rem;
}

.todo-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  padding: 15px;
  background: #f0f4ff;
  border-radius: 6px;
}

.stat {
  flex: 1;
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 5px;
  font-weight: 600;
}

.stat-value {
  display: block;
  font-size: 25px;
  font-weight: 700;
  color: #667eea;
}
.stat-value.inprogress {
  color: blueviolet;
}
.stat-value.completed {
  color: green;
}
.stat-value.blocked {
  color: red;
}

.stat-value.todo {
  color: grey;
}

.todo-list {
  list-style: none;
}

.todo-item {
  display: flex;
  align-items: center;
  padding: 15px;
  margin-bottom: 10px;
  background: white;
  border: 1px solid #eee;
  border-radius: 6px;
  transition: all 0.3s;
}

.todo-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #ddd;
}

.todo-item.completed {
  background: #f5f5f5;
  opacity: 0.7;
}

.todo-item.completed .todo-title {
  text-decoration: line-through;
  color: #999;
}

.todo-content {
  flex: 1;
  min-width: 0;
}

.todo-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 5px;
}

.todo-checkbox {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: #667eea;
}

.todo-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  flex: 1;
}

.todo-priority {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
}

.priority-1 {
  background: #fadbd8;
  color: red;
}

.priority-2 {
  background: #fef5e7;
  color: orange;
}

.priority-3 {
  background: #d5f4e6;
  color: green;
}

.todo-description {
  margin: 8px 0 0 30px;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
}

.tags{
   margin: 8px 0 0 30px;
}

.todo-tag {
  color: #666;
}

.todo-actions {
  display: flex;
  gap: 8px;
  margin-left: 10px;
}

.btn-icon {
  width: 50px;
  height: 36px;
  border: none;
  background: #f0f0f0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.1rem;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-edit:hover {
  background: #667eea;
  transform: scale(1.1);
}

.btn-delete:hover {
  background: #e74c3c;
  transform: scale(1.1);
}
</style>
