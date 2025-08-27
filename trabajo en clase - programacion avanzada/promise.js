//asincronismo
//promises, se usan para llamados asincronicos
// usa el resolve para cuando el llamado es correcto
// y el reject cuando hay un error

const aplicardescuento = new Promise((resolve, reject) => {

    setTimeout(() => {
        let descuento = true
        if (descuento) {
            resolve("Descuento aplicado")
        } else {
            reject("Pelotudo")
        }
    }, 3000)

})

aplicardescuento.then(resultado => {
    console.log(resultado);
}).catch(error => {
    console.log("hubo un error mega nasheeeeeeeeeeeeeee en la consulta" + error);
})
//usamos el catch para devolverle el error al usuario en este caso
// 