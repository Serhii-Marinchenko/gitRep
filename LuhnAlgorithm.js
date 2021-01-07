// All valid credit card numbers
const valid1 = [4, 5, 3, 9, 6, 7, 7, 9, 0, 8, 0, 1, 6, 8, 0, 8];
const valid2 = [5, 5, 3, 5, 7, 6, 6, 7, 6, 8, 7, 5, 1, 4, 3, 9];
const valid3 = [3, 7, 1, 6, 1, 2, 0, 1, 9, 9, 8, 5, 2, 3, 6];
const valid4 = [6, 0, 1, 1, 1, 4, 4, 3, 4, 0, 6, 8, 2, 9, 0, 5];
const valid5 = [4, 5, 3, 9, 4, 0, 4, 9, 6, 7, 8, 6, 9, 6, 6, 6];

// All invalid credit card numbers
const invalid1 = [4, 5, 3, 2, 7, 7, 8, 7, 7, 1, 0, 9, 1, 7, 9, 5];
const invalid2 = [5, 7, 9, 5, 5, 9, 3, 3, 9, 2, 1, 3, 4, 6, 4, 3];
const invalid3 = [3, 7, 5, 7, 9, 6, 0, 8, 4, 4, 5, 9, 9, 1, 4];
const invalid4 = [6, 0, 1, 1, 1, 2, 7, 9, 6, 1, 7, 7, 7, 9, 3, 5];
const invalid5 = [5, 3, 8, 2, 0, 1, 9, 7, 7, 2, 8, 8, 3, 8, 5, 4];

// Can be either valid or invalid
const mystery1 = [3, 4, 4, 8, 0, 1, 9, 6, 8, 3, 0, 5, 4, 1, 4];
const mystery2 = [5, 4, 6, 6, 1, 0, 0, 8, 6, 1, 6, 2, 0, 2, 3, 9];
const mystery3 = [6, 0, 1, 1, 3, 7, 7, 0, 2, 0, 9, 6, 2, 6, 5, 6, 2, 0, 3];
const mystery4 = [4, 9, 2, 9, 8, 7, 7, 1, 6, 9, 2, 1, 7, 0, 9, 3];
const mystery5 = [4, 9, 1, 3, 5, 4, 0, 4, 6, 3, 0, 7, 2, 5, 2, 3];

// An array of all the arrays above
const batch = [valid1, valid2, valid3, valid4, valid5, invalid1, invalid2, invalid3, invalid4, invalid5, mystery1, mystery2, mystery3, mystery4, mystery5];


// helper functions
const hd = x => x[0]
const tl = x => x.slice(1)
// Implementing Luhn algorithm. Return true if card is valid
function validateCred(arr) {
  let arr1 = []
  for (let i in arr) {
    arr1[arr.length-i-1] = arr[i] // arr1 is reversed version of arr
  }
  function aux (arr, i) {
    if (arr.length === 0) {
      return 0
    } else if (i % 2 === 0) {
    let head = ((hd(arr)*2 > 9)? (hd(arr)*2-9):
    (hd(arr)*2))
  //  console.log(head)
    return head + aux(tl(arr), i+1)
  } else {
  //  console.log(hd(arr))
    return hd(arr) + aux(tl(arr), i+1)
  }
  }
  const sum = aux(tl(arr1), 0) + hd(arr1)
  return sum % 10 === 0
}
//console.log(validateCred(invalid5))

/* Takes one parameter for a nested array of credit card numbers.
Check through the nested array for which numbers are invalid, and return another nested array of invalid cards. */
const findInvalidCards = arr => arr.filter(x => !validateCred(x))

//console.log(findInvalidCards([valid1, valid3, invalid1]))

function idInvalidCardCompanies (arr) { //Has one parameter for a nested array of invalid numbers and returns an array of corresponding companies.
    const firstDigits = [3, 4, 5, 6]
    const companies = ['Amex (American Express)', 'Visa', 'Mastercard', 'Discover']
    let ans = []
    function aux (arr) {
	if (arr.length === 0) {
	    return ans
	} else {
	    const first = hd(hd(arr))
	    for (let i in firstDigits) {
		if (first === firstDigits[i] && !ans.includes(companies[i])) {
		    ans.push(companies[i])
		}
	    }
	    return aux(tl(arr))
	}
    }
    return aux(arr)
}

console.log(idInvalidCardCompanies(batch))


