//Lógica: pegar todos os elementos .book e abrir modal com os dara-attributes
// Lógica: pegar todos os elementos .book e abrir modal com os data-attributes
    const books = document.querySelectorAll('.book');
    const modalBackdrop = document.getElementById('modalBackdrop');
    const modalTitle = document.getElementById('modalTitle');
    const modalAuthor = document.getElementById('modalAuthor');
    const modalDesc = document.getElementById('modalDesc');
    const modalImg = document.getElementById('modalImg');
    const openLinkBtn = document.getElementById('openLink');
    const closeModalBtn = document.getElementById('closeModal');

    let currentLink = '#';

    books.forEach(book => {
      book.addEventListener('click', () => {
        const title = book.dataset.title;
        const author = book.dataset.author;
        const desc = book.dataset.desc;
        const img = book.dataset.img;
        const link = book.dataset.link;

        modalTitle.textContent = title;
        modalAuthor.textContent = author;
        modalDesc.textContent = desc;
        modalImg.src = img;
        modalImg.alt = 'Capa ' + title;
        currentLink = link || '#';

        modalBackdrop.style.display = 'flex';
        modalBackdrop.setAttribute('aria-hidden','false');
      });
    });

    // abrir link em nova aba
    openLinkBtn.addEventListener('click', () => {
      if (currentLink && currentLink !== '#') {
        window.open(currentLink, '_blank');
      } else {
        alert('Nenhum link configurado para este livro.');
      }
    });

    // fechar modal
    closeModalBtn.addEventListener('click', closeModal);
    modalBackdrop.addEventListener('click', (e) => {
      if (e.target === modalBackdrop) closeModal();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeModal();
    });

    function closeModal() {
      modalBackdrop.style.display = 'none';
      modalBackdrop.setAttribute('aria-hidden','true');
    }