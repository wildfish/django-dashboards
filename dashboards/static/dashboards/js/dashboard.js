// since we ar currently shipping very little js lets just include it here
// but if this grows we will need to add a build step to create a nice bundle
const setAppearance = (mode) => {
    console.log(document.cookie)

    const d = new Date();
    d.setTime(d.getTime() + (100 * 24 * 60 * 60 * 1000));
    document.cookie = `appearanceMode=${mode}; expires=${d.toString()}; path=/`

    document.body.classList.remove("dark")
    document.body.classList.remove("light")
    if (mode) {
        document.body.classList.add(mode)
    }
    console.log(document.cookie)
}

const Dashboard = {
    setAppearance,
}