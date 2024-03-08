/* Récupérer le nom de la class 'update-cart' */

var updateBtns = document.getElementsByClassName('update-cart')


/* Récupérer l'ID du produit à chaque click et l'ajouter*/


for(var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)
        /* vérifier dans la console si les données ont été correctement envoyé lors du click (voir view aussi updateItem */
        console.log('USER:', user)
        if(user === 'AnonymousUser'){
             addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function addCookieItem(productId, action){
    console.log('Not logged in..')

    if(action === 'add'){
        if(cart[productId] === undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if(action === 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('Remove Item')
            delete cart[productId]
        }
    }
    console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

/* Fonction pour mettre à jour la commande de l'utilisateur */
function updateUserOrder(productId, action){
    console.log('User is logged in, sendind data..')

    var url = '/update_item/' /* Update_Item c'est mise à jour de l'article*/
/* Nous voulons envoyer les données de produits ou aticle lors du click vers le backend*/
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
             'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action':action}) /* Données envoyées sous forme objet*/
    })

        .then((response) =>{  /* Accusé de réception défini dans view updateItem*/
        return response.json()
    })

        .then((data) =>{
            console.log('data:', data) /* Récupération des données*/
            location.reload()
    })
}