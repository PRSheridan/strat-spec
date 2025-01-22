import { Outlet, useLocation } from "react-router-dom"
import "./App.css"

import NavBar from './components/NavBar'
import SearchForm from './components/SearchForm'

function App() {
const location = useLocation()
const showSearchForm = location.pathname === "/"

  return (
    <>
      <NavBar />
      {showSearchForm && <SearchForm />}

      <main>
        <Outlet />
      </main>
    </>
  )
}

export default App
