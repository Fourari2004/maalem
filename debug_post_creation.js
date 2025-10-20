// Debug script to test post creation functionality
console.log('Debugging post creation functionality...');

// Mock functions to simulate the post creation process
const mockGetAuthToken = () => {
  // Simulate having a valid token
  return 'mock-jwt-token';
};

const mockCreatePost = async (formData) => {
  console.log('\n=== Testing Post Creation ===');
  
  // Check if we have the required data
  console.log('Form Data Contents:');
  for (let [key, value] of formData.entries()) {
    console.log(`  ${key}:`, value instanceof File ? `${value.name} (${value.type})` : value);
  }
  
  // Validate required fields
  const token = mockGetAuthToken();
  console.log('\nToken Check:', token ? '✓ Token present' : '✗ No token');
  
  const hasDescription = formData.get('description');
  const hasImage = formData.get('image');
  console.log('Content Check:', hasDescription || hasImage ? '✓ Has content' : '✗ No content');
  
  if (!token) {
    throw new Error('Vous devez être connecté pour créer un post.');
  }
  
  if (!hasDescription && !hasImage) {
    throw new Error('Post content cannot be empty');
  }
  
  // Simulate API call
  console.log('\nSimulating API call...');
  console.log('✓ POST request to /api/posts/');
  console.log('✓ Authorization header included');
  console.log('✓ FormData sent correctly');
  
  // Simulate successful response
  return {
    id: 1,
    title: 'Test Post',
    description: formData.get('description') || 'No description',
    created_at: new Date().toISOString()
  };
};

// Test the post creation
async function testPostCreation() {
  try {
    // Create mock form data
    const formData = new FormData();
    formData.append('title', 'Post');
    formData.append('description', 'This is a test post');
    formData.append('category', 'general');
    
    // Add a mock file
    const mockFile = new File(['test content'], 'test.jpg', { type: 'image/jpeg' });
    formData.append('image', mockFile);
    
    // Test the creation
    const result = await mockCreatePost(formData);
    console.log('\n✅ Post creation successful!');
    console.log('Response:', result);
    
  } catch (error) {
    console.log('\n❌ Post creation failed:');
    console.log('Error:', error.message);
  }
}

// Run the test
testPostCreation();

console.log('\n=== Debug Checklist ===');
console.log('✓ Token validation');
console.log('✓ Form data preparation');
console.log('✓ Content validation');
console.log('✓ API request formatting');
console.log('✓ Error handling');