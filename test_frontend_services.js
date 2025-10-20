// Test the actual frontend service functions
const testFrontendServices = async () => {
  try {
    console.log('Testing frontend service functions...');
    
    // Simulate the service functions from posts.js
    const API_URL = process.env.VITE_API_URL || 'http://localhost:8000/api';
    console.log('Using API URL:', API_URL);
    
    // Test getPosts function (simplified version)
    const getPosts = async () => {
      try {
        const response = await fetch(`${API_URL}/posts/`, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
          }
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
      } catch (error) {
        console.error('Error in getPosts:', error);
        throw error;
      }
    };
    
    // Test the function
    console.log('Testing getPosts function...');
    const posts = await getPosts();
    console.log('✅ SUCCESS: getPosts function works!');
    console.log('Received:', Array.isArray(posts) ? `${posts.length} posts` : typeof posts);
    
  } catch (error) {
    console.log('❌ ERROR: Frontend services test failed');
    console.log('Error message:', error.message);
  }
};

// Run the test
testFrontendServices();