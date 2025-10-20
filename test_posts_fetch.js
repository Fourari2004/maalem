// Test script to verify that the frontend can fetch posts
const testPostsFetch = async () => {
  try {
    console.log('Testing posts fetch from frontend...');
    
    // Simulate the environment variable that would be available in the frontend
    const VITE_API_URL = 'http://localhost:8000/api';
    const API_URL = VITE_API_URL || 'http://localhost:8000/api';
    
    console.log('Using API URL:', API_URL);
    
    // Test the actual getPosts function logic
    const getAuthToken = () => {
      // In a real scenario, this would get the token from localStorage
      return null; // No auth for this test
    };
    
    const token = getAuthToken();
    const headers = {
      'Accept': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    };
    
    console.log('Making request to:', `${API_URL}/posts/`);
    console.log('Headers:', headers);
    
    const response = await fetch(`${API_URL}/posts/`, {
      method: 'GET',
      headers: headers
    });
    
    console.log('Response status:', response.status);
    console.log('Response OK:', response.ok);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const contentType = response.headers.get('content-type');
    console.log('Content type:', contentType);
    
    if (!contentType || !contentType.includes('application/json')) {
      throw new Error('Received non-JSON response from server');
    }
    
    const data = await response.json();
    console.log('✅ SUCCESS: Posts fetched successfully!');
    console.log('Data type:', Array.isArray(data) ? 'Array' : typeof data);
    console.log('Data length:', Array.isArray(data) ? data.length : 'N/A');
    
  } catch (error) {
    console.log('❌ ERROR: Failed to fetch posts');
    console.log('Error name:', error.name);
    console.log('Error message:', error.message);
    console.log('This might be due to:');
    console.log('1. Backend server not running');
    console.log('2. Network connectivity issues');
    console.log('3. CORS configuration problems');
    console.log('4. API endpoint not available');
  }
};

// Run the test
testPostsFetch();