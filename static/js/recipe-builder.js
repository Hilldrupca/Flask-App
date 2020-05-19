var ingredients = 0;
var foodsearch = [];
var timer = 0;

function nextIng(){
    var next = ingredients;
    ingredients++;
    return 'item'+next.toString()
};

function search(){
    var a = new XMLHttpRequest();
    var term = document.getElementById('foodsearch').value;
    if (term){
        a.open('GET','/search/'+term,true);
        a.onload = function(){
            if (a.readyState == 4 && a.status == 200){
                foodsearch = JSON.parse(this.responseText);
                autocomplete();
            };
        };
        a.send();
    }else{
        closeAutocomplete();
    }
};

function delay(input){
    input.addEventListener('input', function(){
        if(timer){clearTimeout(timer)};
        timer = setTimeout(search,1000);
    });
    input.addEventListener('click', function(){
        if(timer){clearTimeout(timer)};
        timer = setTimeout(search,1000);
    });
    document.addEventListener('click', closeAutocomplete());
    
};

function autocomplete(){
    closeAutocomplete();
    a = document.createElement('DIV');
    a.setAttribute('class', 'autocomplete-items');
    document.getElementById('foodsearch').parentNode.appendChild(a);
        
    for (i = 0; i < foodsearch.length; i++){
        b = document.createElement('DIV');
        b.innerHTML = foodsearch[i].name;
        b.addEventListener('click', function(e){
            input.value = this.innerHTML;
            closeAutocomplete();
        });
        a.appendChild(b);
    };
}

function closeAutocomplete(){
    var a = document.getElementsByClassName('autocomplete-items');
    for (i = 0; i < a.length; i++){
        a[i].parentNode.removeChild(a[i]);
    };
};
        
function resetRow(row){
    var rowId = parseInt(row.slice(-1));
    var item = 'item' + rowId;
    var amount = 'amount' + rowId;
    var unit = 'unit' + rowId;
    document.getElementById(item).innerHTML = '';
    document.getElementById(amount).value = 0;
    shiftRow(rowId);
    ingredients--;
};

function shiftRow(rowId){
    var tablerows = document.getElementById('foodtable').rows.length;
    for (i = rowId; i < tablerows-1; i++){
        var next = i+1;
        document.getElementById('item'+i).innerHTML = document.getElementById('item'+next).innerHTML;
        document.getElementById('amount'+i).value = document.getElementById('amount'+next).value;
    }
    tablerows--;
    document.getElementById('item'+tablerows).innerHTML='';
    document.getElementById('amount'+tablerows).value=0;
};

