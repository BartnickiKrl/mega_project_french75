const maxPeople = 10;
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
        alert("Maximum 10 users are allowed");
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

function disableButton(form) {

    if (form.checkValidity()) {
        const btn = document.getElementById('submit-btn');
        
        // Blokada przycisku z lekkim opóźnieniem tylko wtedy, gdy dane są poprawne
        setTimeout(function() {
            btn.disabled = true;
            btn.style.opacity = "0.5";
            btn.style.cursor = "not-allowed";
            btn.innerHTML = '<span class="loader"></span> Looking through your watchlists...';
        }, 50);

        return true; // Formularz zostanie wysłany
    } else {
        return false; 
    }
}

setTimeout(function() {
    let messages = document.querySelectorAll('.messages li');
    
    messages.forEach((msg, index) => {
        // Dodajemy lekkie opóźnienie dla każdego kolejnego elementu (efekt kaskady)
        setTimeout(() => {
            msg.classList.add('hide');
            
            // Usuwamy element z DOM dopiero po zakończeniu animacji CSS
            setTimeout(() => {
                msg.remove();
            }, 500); 
        }, index * 200); // Pierwszy znika od razu, następny 200ms później
    });
}, 1400);