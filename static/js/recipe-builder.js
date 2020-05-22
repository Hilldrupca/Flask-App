var ingredients = 0;
var foodsearch = [];
var foodlist = [];
var test = [{'hi':12}];
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
        a.open('GET','/foodsearch/'+term,true);
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
    document.addEventListener('click', closeAutocomplete);
};

function autocomplete(){
    closeAutocomplete();
    if (foodsearch.length){
        a = document.createElement('DIV');
        a.setAttribute('class', 'autocomplete-items');
        a.setAttribute('style', 'margin: 0px 0px 0px 20%;');
        document.getElementById('foodsearch').parentNode.appendChild(a);
    };
    for (i = 0; i < foodsearch.length; i++){
        b = document.createElement('DIV');
        b.innerHTML = foodsearch[i].name;
        b.id = foodsearch[i].code;
        b.addEventListener('click', function(e){
            input.value = this.innerHTML;
            input.name = this.id;
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
    var rowId = parseInt(row.id.slice(-1));
    var item = 'item' + rowId;
    if (document.getElementById(item).innerHTML){
        var amount = 'amount' + rowId;
        var unit = 'unit' + rowId;
        document.getElementById(item).innerHTML = '';
        document.getElementById(amount).value = 0;
        updateFood(row);
        shiftRow(rowId);
        ingredients--;
    }
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

function addFood(){
    item = document.getElementById('item' + ingredients);
    food = document.getElementById('foodsearch');
    
    var a = new XMLHttpRequest();
    a.open('GET', '/nutritiondata/' + food.name, true);
    a.onload = function(){
        if (a.readyState == 4 && a.status == 200){
            item.innerHTML = food.value;
            foodlist.push(JSON.parse(a.responseText));
            foodlist[ingredients].amount=0;
            foodlist[ingredients].code=food.name.toString();
            foodlist[ingredients].name=food.value.toString();
            food.value = '';
            food.name = '';
            ingredients++;
        }else{
            alert("Sorry, the food you are searching for isn't in our database.")
        };
    };
    a.send();
};

function updateFood(e){
    var food = foodlist[parseInt(e.id.slice(-1))];
    var diff = e.value - food.amount;
    for (var nut in food){
        if (nut == 'amount'){ break;}
        var currentNut = document.getElementById(nut);
        currentNut.className = parseFloat(currentNut.className) + (diff / 100 * parseFloat(food[nut]));
        currentNut.innerHTML = parseFloat(currentNut.className).toFixed(1);
        if (isNaN(currentNut.innerHTML) || parseFloat(currentNut.innerHTML) == 0){
            currentNut.innerHTML = 0;
            currentNut.className = 0;
        };
        
    };
    food.amount = e.value;
};
