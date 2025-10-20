// Test script to verify button enable/disable logic
console.log('Testing button enable/disable logic...');

// Test cases for button disabled state
const testCases = [
  {
    name: 'Empty form',
    state: { loading: false, postText: '', selectedImages: [] },
    expected: true // should be disabled
  },
  {
    name: 'Only whitespace text',
    state: { loading: false, postText: '   ', selectedImages: [] },
    expected: true // should be disabled
  },
  {
    name: 'Text only',
    state: { loading: false, postText: 'Hello world', selectedImages: [] },
    expected: false // should be enabled
  },
  {
    name: 'Image only',
    state: { loading: false, postText: '', selectedImages: [{}] },
    expected: false // should be enabled
  },
  {
    name: 'Text and images',
    state: { loading: false, postText: 'Hello world', selectedImages: [{}] },
    expected: false // should be enabled
  },
  {
    name: 'Loading state',
    state: { loading: true, postText: 'Hello world', selectedImages: [] },
    expected: true // should be disabled
  }
];

console.log('\n=== Button Disabled Logic Tests ===\n');

let passedTests = 0;

testCases.forEach(test => {
  const { loading, postText, selectedImages } = test.state;
  const isDisabled = loading || (!postText.trim() && selectedImages.length === 0);
  
  const result = isDisabled === test.expected ? '✅ PASS' : '❌ FAIL';
  console.log(`${result} ${test.name}`);
  console.log(`  State: loading=${loading}, postText="${postText}", selectedImages=${selectedImages.length}`);
  console.log(`  Disabled: ${isDisabled} (expected: ${test.expected})`);
  console.log('');
  
  if (isDisabled === test.expected) passedTests++;
});

console.log(`\nResults: ${passedTests}/${testCases.length} tests passed`);

if (passedTests === testCases.length) {
  console.log('✅ All tests passed! Button logic is working correctly.');
} else {
  console.log('❌ Some tests failed. There may be an issue with the button logic.');
}

console.log('\n=== Common Issues to Check ===');
console.log('1. Make sure you have entered text OR selected an image');
console.log('2. Check if the loading state is stuck on true');
console.log('3. Verify that image selection is working properly');
console.log('4. Ensure there are no JavaScript errors in the console');