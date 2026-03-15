import axios from 'axios'

// @TODO: TEMPORARY DIRECT ASSIGNMENT FOR DEMO PURPOSE ONLY - BRYLLE 
// ENVIRONMENT VARIABLES MUST BE STORE IN SECRECTS
const API_BASE_URL = 'http://localhost:8004/api'

const todoService = {
  // Get all todos
  getTodos() {
    return axios.get(`${API_BASE_URL}/todo/`)
  },

  // Get single todo
  getTodo(todoId) {
    return axios.get(`${API_BASE_URL}/todo/${todoId}`)
  },

  // Create new todo
  createTodo(todoData) {
    return axios.post(`${API_BASE_URL}/todo/`, todoData)
  },

  // Update todo (partial)
  updateTodo(todoId, todoData) {
    return axios.patch(`${API_BASE_URL}/todo/${todoId}`, todoData)
  },

  // Delete todo
  deleteTodo(todoId) {
    return axios.delete(`${API_BASE_URL}/todo/${todoId}`)
  }
}

export default todoService
