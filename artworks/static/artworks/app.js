


const FoldWrapper = ({ headline, closed = true, children }) => {
    return (
        <section>
            <div className="fold-container">
                <div className="headline-container">
                    <h2>{headline}</h2>
                    <i className={`bi ${closed ? 'bi-caret-down' : 'bi-caret-up'}`} />
                </div>
                <div className={`fold-content ${closed ? 'hidden' : 'visible'}`}>
                    {children}
                </div>
            </div>
        </section>
    )

}

const About = () => {
    return (
        <FoldWrapper headline="About">
                <p>This project is a "gift" for my cronically ill mother who loves to paint. </p>
                <p>It is a part of a fully working application where Django and python serves as a REST API and for authentication and Security. The backend communicates with a PostgreSQL database, and the frontend is a separate application written in React and TypeScript.</p>
                <p>The project is hosted on Heroku, and uses HostUp as a domain registrar. I have also used Github actions to create a CI/CD pipeline that deploys the app to Heroku on push to main.</p>
        </FoldWrapper>
    )
}

const Links = () => {
    return (
        <FoldWrapper headline="Links">
            <div className="link-container">
                <span className="bold">Backend applikation: </span>
                <a href="http://api.gunilla-arno-toll.se" target="_blank">api.gunilla-arno-toll.se</a>
            </div>
            <div className="link-container">
                <span className="bold">Backend repo: </span>
                <a href="https://github.com/AnnaToll/artworks-server" target="_blank">Github</a>
            </div>
            <div className="link-container">
                <span className="bold">Frontend applikation: </span>
                <a href="http://gunilla-arno-toll.se" target="_blank">gunilla-arno-toll.se</a>
            </div>
            <div className="link-container">
                <span className="bold">Frontend repo: </span>
                <a href="https://github.com/AnnaToll/artworks-app" target="_blank">Github</a>
            </div>
        </FoldWrapper>
    )
}


const Images = () => {

    const location = window.location.href

    const ImagesArr = () => {
        const newArr = []
        for (let i = 1; i < 10; i++) {
            newArr.push(
                <div className="image-container" key={'image' + i}>
                    <img src={`${location}static/artworks/img/${i}.png`} />
                </div>   
            )
        }
        return newArr
    }

    return (
        <FoldWrapper headline="Images" closed={false}>
            <div id="images-container">
                {ImagesArr()}
            </div>
        </FoldWrapper>
    )

}


const App = () => {
    return (
        <main>
            <section id="about-container">
                <h1>Fully functional backend for CMS</h1>
                <p id="intro">REST API, security, PostgreSQL, CI/CD-Pipeline, etc.</p>
                <About />
                <Links />
                <Images />
            </section>
        </main>
    )
}

const root = document.querySelector('#root')

ReactDOM.render(<App/>, root)

const headlineContainers = document.querySelectorAll('.headline-container')
console.log(headlineContainers)
headlineContainers.forEach(headlineContainer => {
    console.log(headlineContainer)
    headlineContainer.addEventListener('click', () => {
        const caret = headlineContainer.children[1]
        const contentContainer = headlineContainer.nextElementSibling

        if (caret.classList.contains('bi-caret-down')) {
            caret.classList.remove('bi-caret-down')
            caret.classList.add('bi-caret-up')
        } else {
            caret.classList.remove('bi-caret-up')
            caret.classList.add('bi-caret-down')
        }

        if (contentContainer.classList.contains('visible')) {
            contentContainer.classList.remove('visible')
            contentContainer.classList.add('hidden')
        } else {
            contentContainer.classList.remove('hidden')
            contentContainer.classList.add('visible')
        }
    })
})