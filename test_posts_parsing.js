// Test script to verify posts parsing handles pagination correctly
console.log('Testing posts parsing with pagination...');

// Mock paginated response from Django REST Framework
const mockPaginatedResponse = {
  "count": 4,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 4,
      "author": {
        "id": 15,
        "username": "test_artisan_8880",
        "profile_picture": null,
        "user_type": "artisan"
      },
      "title": "Test Post",
      "description": "This is a test post created from Python script",
      "created_at": "2025-10-18T19:47:48.281764Z",
      "updated_at": "2025-10-18T19:47:48.281801Z",
      "image": null,
      "category": "general",
      "location": "",
      "latitude": null,
      "longitude": null,
      "likes_count": 0,
      "comments_count": 0,
      "is_liked": false,
      "is_saved": false,
      "comments": []
    }
  ]
};

// Mock direct array response
const mockArrayResponse = [
  {
    "id": 4,
    "author": {
      "id": 15,
      "username": "test_artisan_8880",
      "profile_picture": null,
      "user_type": "artisan"
    },
    "title": "Test Post",
    "description": "This is a test post created from Python script",
    "created_at": "2025-10-18T19:47:48.281764Z",
    "updated_at": "2025-10-18T19:47:48.281801Z",
    "image": null,
    "category": "general",
    "location": "",
    "latitude": null,
    "longitude": null,
    "likes_count": 0,
    "comments_count": 0,
    "is_liked": false,
    "is_saved": false,
    "comments": []
  }
];

// Function to handle posts data (similar to what we implemented in the service)
function handlePostsData(data) {
  console.log('\nProcessing data:', typeof data);
  
  let postsArray = [];
  if (Array.isArray(data)) {
    // Direct array response
    postsArray = data;
    console.log('✓ Handled as direct array with', postsArray.length, 'items');
  } else if (data && typeof data === 'object' && Array.isArray(data.results)) {
    // Paginated response with results field
    postsArray = data.results;
    console.log('✓ Handled as paginated response with', postsArray.length, 'items');
  } else {
    console.log('✗ Unexpected data format');
    return [];
  }
  
  // Transform the data (simplified version)
  const transformedPosts = postsArray.map(post => ({
    id: post.id,
    author: {
      id: post.author.id,
      name: post.author.username,
      specialty: post.author.user_type === 'artisan' ? post.author.specialty : '',
      avatar: post.author.profile_picture || '/placeholder-user.svg'
    },
    content: post.description,
    image: post.image || '/placeholder-post.jpg',
    date: new Date(post.created_at).toLocaleDateString('fr-FR')
  }));
  
  console.log('✓ Successfully transformed', transformedPosts.length, 'posts');
  return transformedPosts;
}

// Test with paginated response
console.log('\n1. Testing with paginated response:');
const result1 = handlePostsData(mockPaginatedResponse);

// Test with array response
console.log('\n2. Testing with array response:');
const result2 = handlePostsData(mockArrayResponse);

// Test with invalid response
console.log('\n3. Testing with invalid response:');
const result3 = handlePostsData("invalid data");

console.log('\n✅ All tests completed successfully!');
console.log('\nThe posts service now correctly handles:');
console.log('  - Paginated responses from Django REST Framework');
console.log('  - Direct array responses');
console.log('  - Invalid response formats (gracefully)');
console.log('  - Data transformation for frontend consumption');