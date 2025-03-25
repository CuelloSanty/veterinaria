document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById("miDibujo");
    const ctx = canvas.getContext("2d");

    // Ajuste de las posiciones para que los dedos queden alineados
    const posiciones = [
        { x: 130, y: 200, rX: 20, rY: 32 }, // Dedo 1
        { x: 170, y: 150, rX: 26, rY: 40 }, // Dedo 2
        { x: 230, y: 150, rX: 26, rY: 40 }, // Dedo 3
        { x: 270, y: 200, rX: 20, rY: 32 }, // Dedo 4
        { x: 200, y: 250, rX: 50, rY: 55 }  // Palma (base)
    ];

    let paso = 0;

    function dibujar() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "rgb(162, 201, 238)";

        for (let i = 0; i <= paso; i++) {
            if (i < posiciones.length) {
                ctx.beginPath();
                ctx.ellipse(posiciones[i].x, posiciones[i].y, posiciones[i].rX, posiciones[i].rY, 0, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        if (paso < posiciones.length - 1) {
            paso++;
            setTimeout(dibujar, 400);
        }
    }

    dibujar();
});