import { Outlet, useLocation } from "react-router-dom"
import "./App.css"

import NavBar from './components/NavBar'
import SearchForm from './components/forms/SearchForm'
import { GuitarProvider } from "./context/GuitarContext"

function App() {
const location = useLocation()
const showSearchForm = location.pathname === "/"

  return (
    <>
      <NavBar />
      {showSearchForm && <SearchForm />}

      <main>
        <GuitarProvider >
          <Outlet />
        </GuitarProvider>
      </main>
    </>
  )
}

export default App
