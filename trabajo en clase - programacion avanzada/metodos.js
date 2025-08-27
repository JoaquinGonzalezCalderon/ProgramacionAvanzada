//metodos en arreglos 

const personas = [

    { nombre: "juan", edad: 25, aprendiendo: "python" },
    { nombre: "jorge", edad: 54, aprendiendo: "js" },
    { nombre: "leandro", edad: 22, aprendiendo: "java" },
    { nombre: "gaspar", edad: 98, aprendiendo: "ingles" }

]

console.log(personas);

const mayores = personas.filter(persona => persona.edad > 24);

console.log("Personas mayores a 28: ", mayores);


const personas2 = [

    { nombre: "joaquin", edad: 56, aprendiendo: "python" },
    { nombre: "pedro", edad: 23, aprendiendo: "js" },
    { nombre: "rosa", edad: 65, aprendiendo: "java" },
    { nombre: "alfredo", edad: 54, aprendiendo: "ingles" }

]

// filtrado con concatenado de tablas

const filtrado = [...personas, ...personas2].filter(persona => persona.edad > 28);

console.log("Personas de ambas tablas mayores de 28: ", filtrado)
