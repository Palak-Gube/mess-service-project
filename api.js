// Simple API utility - All backend calls in one place
const API_BASE = 'http://localhost:5000/api';

// Helper function for API calls
async function apiCall(endpoint, method = 'GET', data = null) {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (data) options.body = JSON.stringify(data);
  
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, options);
    const result = await res.json();
    
    // Convert technical errors to user-friendly messages
    if (result.error) {
      let errorMsg = result.error;
      
      if (errorMsg.includes('UNIQUE constraint failed')) {
        if (errorMsg.includes('student_id')) {
          errorMsg = 'This Student ID is already registered. Please use a different ID or leave it blank.';
        } else if (errorMsg.includes('email')) {
          errorMsg = 'This email is already registered. Please use a different email.';
        } else if (errorMsg.includes('username')) {
          errorMsg = 'This username is already taken. Please choose a different username.';
        } else {
          errorMsg = 'This information is already registered. Please check your details.';
        }
      }
      
      result.error = errorMsg;
    }
    
    return result;
  } catch (error) {
    console.error('API Error:', error);
    return { 
      success: false,
      error: 'Unable to connect to server. Please check if the server is running.' 
    };
  }
}

// Authentication
const auth = {
  login: (role, username, password) => apiCall('/login', 'POST', { role, username, password }),
  register: async (data) => {
    try {
      const result = await apiCall('/register', 'POST', data);
      return result;
    } catch (error) {
      // Handle network errors
      return { 
        success: false, 
        error: 'Unable to connect to server. Please check your internet connection and try again.' 
      };
    }
  },
};

// Student operations
const student = {
  getProfile: (id) => apiCall(`/students/${id}`),
  updateProfile: (id, data) => apiCall(`/students/${id}`, 'PUT', data),
  submitFeedback: (id, feedback) => apiCall(`/students/${id}/feedback`, 'POST', { feedback }),
  getSubscriptions: (id) => apiCall(`/students/${id}/subscriptions`),
  selectPackage: (id, packageId) => apiCall(`/students/${id}/subscriptions`, 'POST', { packageId }),
  markAttendance: (id, date, mealType) => apiCall(`/students/${id}/attendance`, 'POST', { date, mealType }),
  getAttendance: (id) => apiCall(`/students/${id}/attendance`),
};

// Admin operations
const admin = {
  getAllFeedbacks: () => apiCall('/admin/feedbacks'),
  getAllSubscriptions: () => apiCall('/admin/subscriptions'),
  markStudentAttendance: (studentId, date, mealType) => apiCall('/admin/attendance', 'POST', { studentId, date, mealType }),
  getAttendanceReport: (date) => apiCall(`/admin/attendance?date=${date}`),
  updateAttendance: (attendanceId, data) => apiCall(`/admin/attendance/${attendanceId}`, 'PUT', data),
  deleteAttendance: (attendanceId) => apiCall(`/admin/attendance/${attendanceId}`, 'DELETE'),
  getDashboard: (studentIds = []) => {
    let endpoint = '/admin/dashboard';
    if (studentIds.length > 0) {
      endpoint += '?student_ids=' + studentIds.join(',');
    }
    return apiCall(endpoint);
  },
};

// Menu & Packages
const menu = {
  getTodayMenu: () => apiCall('/menu/today'),
  getPackages: () => apiCall('/packages'),
  getAllMenuItems: () => apiCall('/admin/menu'),
  createMenuItem: (data) => apiCall('/admin/menu', 'POST', data),
  updateMenuItem: (id, data) => apiCall(`/admin/menu/${id}`, 'PUT', data),
  deleteMenuItem: (id) => apiCall(`/admin/menu/${id}`, 'DELETE'),
};

// Additional Admin operations
admin.getAllStudents = () => apiCall('/admin/students');

// Billing
const billing = {
  getBills: (studentId) => apiCall(`/students/${studentId}/bills`),
};


