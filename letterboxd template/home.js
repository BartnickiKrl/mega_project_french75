const maxPeople = 12;
const minPeople = 2;
const container = document.getElementById('fiszki-wrapper');
const addBtn = document.getElementById('add-person');
const removeBtn = document.getElementById('remove-person');

addBtn.addEventListener('click', () => {
    const currentPeople = container.querySelectorAll('.fiszka').length;
    
    if (currentPeople < maxPeople) {

        const firstFiszka = container.querySelector('.fiszka');
        const newFiszka = firstFiszka.cloneNode(true);
        
        const input = newFiszka.querySelector('input');
        input.value = '';
        
        container.appendChild(newFiszka);
    } else {
        alert("Maximum 12 users are allowed");
    }
});

removeBtn.addEventListener('click', () => {
    const people = container.querySelectorAll('.fiszka');
    
    if (people.length > minPeople) {
        container.removeChild(people[people.length - 1]);
    } else {
        alert("Minimum 2 users are required");
    }
});