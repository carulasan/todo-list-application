<template>
  <div class="app-container">
    <div class="app-wrapper">
      <header class="app-header">
        <h4> Geoplan Todo List Application</h4>
        <p class="subtitle">Brylle Technical Exam</p>
      </header>

      <main class="app-main">
        <TodoForm @todo-created="handleTodoCreated" />
        <TodoList 
          :todos="todos" 
          @todo-updated="handleTodoUpdated"
          @todo-deleted="handleTodoDeleted"
        />
      </main>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import TodoForm from './components/TodoForm.vue'
import TodoList from './components/TodoList.vue'
import todoService from './api/todoService'

export default {
  name: 'App',
  components: {
    TodoForm,
    TodoList
  },
  setup() {
    const todos = ref([])
    const loading = ref(false)
    const error = ref(null)

    const fetchTodos = async () => {
      loading.value = true
      error.value = null
      try {
        const response = await todoService.getTodos()
        todos.value = response.data.results || []

      } catch (err) {
        console.error('Error fetching todos:', err)
        error.value = 'Failed to fetch todos'
      } finally {
        loading.value = false
      }
    }

    const handleTodoCreated = async () => {
      await fetchTodos()
    }

    const handleTodoUpdated = async () => {
      await fetchTodos()
    }

    const handleTodoDeleted = async () => {
      await fetchTodos()
    }

    onMounted(() => {
      fetchTodos()
    })

    return {
      todos,
      loading,
      error,
      handleTodoCreated,
      handleTodoUpdated,
      handleTodoDeleted
    }
  }
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.app-wrapper {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 600px;
  overflow: hidden;
}

.app-header {
  background: yellow;
  color: black;
  padding: 40px 30px;
  text-align: center;
}

.app-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  font-weight: 700;
}

.subtitle {
  font-size: 1rem;
  opacity: 0.9;
  font-weight: 300;
}

.app-main {
  padding: 30px;
}
</style>
