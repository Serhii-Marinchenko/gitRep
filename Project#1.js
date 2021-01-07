function mixed_messages () {
const Bugs_Bunny = ['Ah, your brother blows bubble gum!', 'Do you happen to know what the penalty is for shooting a fricaseeing rabbit without a fricaseeing rabbit license?', 'Eh, what’s up, doc?', 'Here I go with the timid little woodland creature bit again. It’s shameful, but…ehhh, it’s a living.', 'I’m just a little wabbit!']
const SpongeBob = ['The best time to wear a striped sweater is all the time.', 'F is for friends who do stuff together!', 'If you believe in yourself, with a tiny pinch of magic all your dreams can come true!', 'Is mayonnaise an instrument?']
const Winnie_the_Pooh = ['You’re braver than you believe, stronger than you seem, and smarter than you think.', 'Sometimes the smallest things take up the most room in your heart.', 'I wasn’t going to eat it, I was just going to taste it.', 'I did mean a little larger small helping.']
const characters = ['Bugs_Bunny', 'SpongeBob', 'Winnie_the_Pooh']
function getRandomItem (arg) {
    const random_number = Math.floor(Math.random()*(arg.length-1))
    //console.log(random_number)
    const ans = arg[random_number]
    return ans
    }
    const randomChar = getRandomItem(characters)
    let randomPhrase
    switch (randomChar) {
        case 'Bugs_Bunny':
            randomPhrase = getRandomItem(Bugs_Bunny)
            break;
        case 'SpongeBob':
            randomPhrase = getRandomItem(SpongeBob)
            break;
        case 'Winnie_the_Pooh':
            getRandomItem(Winnie_the_Pooh)
            break;
        default:
            "Programm doesn't work"
            break;
    }
    return `Random ${randomChar}'s quote: "${randomPhrase}"`
}
for (let i = 0; i < 3; i++){
console.log(mixed_messages())
}