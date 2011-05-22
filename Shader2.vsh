attribute vec4 position;

uniform mat4 matriz;
uniform float t;

void main() {
    //La posicion inicial
    vec4 posA = position;
    //La posicion final tras ser rotada 45 grados
    //Es ella misma mas la matriz de transformacion 
    //actuando sobre la posicion inicial
    vec4 posB = position + matriz * position;

    //Cuando t vale 0, estamos en la posicion inicial
    //pues posB se anula
    //Cuando t vale 1 viceversa
    //Por tanto al variar t conseguimos posiciones intermedias
    //entre posA y posB
    vec4 final = t*posB + (1.0-t)*posA;

    gl_Position = gl_ModelViewProjectionMatrix * final;

}
