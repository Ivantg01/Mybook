function deleteBook(book_id) {
    fetch("/delete-book", {
        method: "POST",
        body: JSON.stringify({ book_id: book_id }),
    }).then((_res) => {
        window.location.href = "/";
    });
}