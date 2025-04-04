import { Outlet, useLocation } from "react-router-dom"
import NavBar from './components/NavBar'
import Feed from './pages/Feed'
import { ItemProvider } from "./context/ItemContext"

function App() {
  const location = useLocation()
  const showGuitarFeed = location.pathname === "/"

  return (
    <>
      <NavBar />
      {showGuitarFeed && <Feed />}
      <main>
        <ItemProvider >
          <Outlet />
        </ItemProvider>
      </main>
    </>
  )
}

export default App