// 1. Search bithaaa live
function searchBithaa(){
    let input = document.getElementById('searchInput').value.tolowerCase();
    let rows = document.querySalectorAll('#productTable tbody tr');
    rows.forEach(row => {
        let jina = row.cells[0].innerText.toLowerCase();
        if (jina.includes(input)){
            row.style.display ="";
        }else{
            row.style.display = "none";
        }
    })
} 

// 2. Sauti ya kuuza na Alter ya stock
function uzaBidhaa(jina, stock, id){
    if (stock <= 0){
        alert(jina + " imeishaa!");
        return;
    }

    if (!confirm ("Uza 1 ya " + jina + "?")){
        return;
    }

    // saut
    try{
    let audio = new Audio('https://www.soundjay.com/buttons/sounds/button-3.mp3');
    audio.play().catch(()=>{});
    }catch(e){}    
    
        // alter kama stock itaish
    if (stock <= 5 && stock > 0){
        alert('TAHATHARI: ' + jina + ' imebaki ' + stock + 'tu! Mjulishe Boss!');
        // kuunganisha Whatsapp API
        if (confirm('Utume WhatsApp kwa Boss?')){
            window.open('https://wa.me/255713599104text=Boss, ' + jina + ' imebaki ' + stock + 'tu! dukani!', '_blank');
        }
           
    }
    // Hii inafanyakazi kwa stock kuanzia 1.
    window.location.href= "/uza/" + id + "/";
}

// Uza zaidi ya bidhaa moja kwa pamoja
function uzaZaidi(jina, stock, id){
    if (stock <= 0){
        alert(jina + " imeisha!");
        return;
    }
    let kiasi = prompt("Mteja anataka ngapi za " + jina + "?\nZimebaki " + stock + " dukani:", "1");
    if (kiasi === null) return; //Amecancel

    kiasi = parseInt(kiasi)
    if (isNaN(kiasi) || kiasi <= 0){
        alert("Stock haitoshi! Zimebaki " + stock + " tu!");
        return;
    }

    // sauti ya kuuza
    try{
    let audio = new Audio('https://www.soundjay.com/buttons/sounds/button-3.mp3');
    audio.play().catch(()=>{});
    }catch(e){} 

    // Tuma na idadi
    window.location.href= "/uza/" + id + "/" + kiasi + "/";
}

// 3. Hesabu faida live kwenye form ya kuongeza
function hesabuFaidaLive(){
    let kununua = document.getElementById('bei_kununua').value;
    let kuuza = document.getElementById('bei_kuuza').value;
    if (kununua && kuuza){
        let faida = kuuza - kununua;
        document.getElementById('faidaPreview').innerText = 'Faida: Tsh ' + faida;
    }
}

// 4. Dark mode kwa Boss
function toggleDark(){
    document.body.classList.toggle('bg-dark');
    document.body.classList.toggle('text-white');

}

//5. Auto refresh low stock notification
window.onload = function(){
    let lowItems = document.querySelectorAll('.card-low');
    if (lowIterms.length > 0){
        console.log('Kuna bithaa ' + lowIterms.length + ' zimebaki kidogo!');
    }
}    