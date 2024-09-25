const doneTodo = async (path, is_done) => {
    const response = await fetch(path, {
        method: "POST",
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'is_done=' + is_done
    })

    if (response.redirected) {
        window.location = response.url
    }
}

const deleteTodo = async (path, itemToDelete) => {
    const response = await fetch(path, { method: "POST" })
    const result = response.json()
    if (response.redirected) {
        window.location = response.url
    }
    if (response.ok) {
        itemToDelete.remove()
    } else {
        console.log("Can't delete.")
    }
    return result
}