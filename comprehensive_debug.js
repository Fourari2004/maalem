// Comprehensive debug script for post creation
console.log('=== Comprehensive Post Creation Debug ===\n');

// Mock localStorage to simulate authentication
const mockLocalStorage = {
  authToken: 'mock-jwt-token',
  currentUser: JSON.stringify({ id: 1, username: 'testuser', user_type: 'artisan' })
};

// Mock getAuthToken function
const mockGetAuthToken = () => {
  return mockLocalStorage.authToken;
};

// Mock getCurrentUser function
const mockGetCurrentUser = () => {
  return mockLocalStorage.currentUser ? JSON.parse(mockLocalStorage.currentUser) : null;
};

// Mock isAuthenticated function
const mockIsAuthenticated = () => {
  const token = mockGetAuthToken();
  if (!token) return false;
  
  // Simulate token validation
  try {
    // In a real JWT token, this would be the payload
    // For mocking, we'll just return true if token exists
    return true;
  } catch (e) {
    return false;
  }
};

// Mock isUserArtisan function
const mockIsUserArtisan = () => {
  const user = mockGetCurrentUser();
  return user && user.user_type === 'artisan';
};

console.log('Authentication Status:');
console.log('  Token present:', !!mockGetAuthToken());
console.log('  Authenticated:', mockIsAuthenticated());
console.log('  Is Artisan:', mockIsUserArtisan());

// Test form data creation
console.log('\nForm Data Creation:');
const formData = new FormData();
formData.append('title', 'Post');
formData.append('description', 'Test post content');
formData.append('category', 'general');

const mockFile = new File(['test'], 'test.jpg', { type: 'image/jpeg' });
formData.append('image', mockFile);

console.log('  Form data entries:');
for (let [key, value] of formData.entries()) {
  console.log(`    ${key}:`, value instanceof File ? `${value.name} (${value.type})` : value);
}

// Test createPost function logic
console.log('\nCreate Post Logic:');
const token = mockGetAuthToken();
const hasDescription = formData.get('description');
const hasImage = formData.get('image');

console.log('  Token check:', token ? '✅ Pass' : '❌ Fail');
console.log('  Content check:', (hasDescription || hasImage) ? '✅ Pass' : '❌ Fail');
console.log('  Description:', hasDescription ? `✅ "${hasDescription}"` : '❌ Empty');
console.log('  Image:', hasImage ? `✅ ${hasImage.name}` : '❌ No image');

// Test button enable logic
console.log('\nButton Enable Logic:');
const testStates = [
  { name: 'Empty form', text: '', images: 0, loading: false },
  { name: 'Text only', text: 'Hello', images: 0, loading: false },
  { name: 'Image only', text: '', images: 1, loading: false },
  { name: 'Loading', text: 'Hello', images: 0, loading: true }
];

testStates.forEach(state => {
  const disabled = state.loading || (!state.text.trim() && state.images === 0);
  console.log(`  ${state.name}: ${disabled ? '❌ Disabled' : '✅ Enabled'}`);
});

console.log('\n=== Debug Summary ===');
if (token && (hasDescription || hasImage)) {
  console.log('✅ All prerequisites for post creation are met');
  console.log('   - Authentication token is present');
  console.log('   - Content is available (text or image)');
  console.log('   - Button should be enabled if not loading');
} else {
  console.log('❌ Missing prerequisites for post creation:');
  if (!token) console.log('   - No authentication token');
  if (!(hasDescription || hasImage)) console.log('   - No content (text or image)');
}

console.log('\n=== Troubleshooting Steps ===');
console.log('1. Check browser console for JavaScript errors');
console.log('2. Verify authentication token is present in localStorage');
console.log('3. Ensure you have entered text OR selected an image');
console.log('4. Check if loading state is stuck');
console.log('5. Verify network requests in browser dev tools');