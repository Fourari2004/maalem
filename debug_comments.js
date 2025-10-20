// Debug script to test comment functionality
console.log('=== Comment Debug Script ===');

// Test comment structure
const testComment = {
  id: 1,
  user: {
    id: 1,
    name: 'Test User',
    avatar: '/placeholder-user.svg'
  },
  text: 'This is a test comment',
  date: new Date().toLocaleString('fr-FR')
};

console.log('Test comment structure:', testComment);

// Test comment array
const testComments = [
  testComment,
  {
    id: 2,
    user: {
      id: 2,
      name: 'Another User',
      avatar: '/placeholder-user.svg'
    },
    text: 'This is another test comment',
    date: new Date().toLocaleString('fr-FR')
  }
];

console.log('Test comments array:', testComments);

// Test comment section rendering
console.log('Testing comment section rendering...');

// Check if required elements exist
const requiredElements = [
  'CommentSection',
  'PostCard',
  'addComment',
  'handleAddComment'
];

requiredElements.forEach(element => {
  console.log(`Checking ${element}:`, typeof window[element] !== 'undefined');
});

console.log('=== End Debug Script ===');