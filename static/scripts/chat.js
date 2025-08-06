const rolar = () => {
    const box = document.getElementById('chatBox');
    box.scrollTop = box.scrollHeight;
};

window.onload = rolar;

document.querySelector('form').onsubmit = () => {
    setTimeout(rolar, 100);
};

io().on('atualizar_lista', () => location.reload());