import { Outlet, useLocation } from "react-router-dom"
import NavBar from './components/NavBar'
import Feed from './pages/Feed'
import { GuitarProvider } from "./context/GuitarContext"

function App() {
  const location = useLocation()
  const showGuitarFeed = location.pathname === "/"

  return (
    <>
      <NavBar />
      {showGuitarFeed && <Feed />}
      <main>
        <GuitarProvider >
          <Outlet />
        </GuitarProvider>
      </main>
    </>
  )
}

export default App
