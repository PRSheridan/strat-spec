import { NavLink } from "react-router-dom";

function NavBar () {
  //if logged in show profile and logout
    return (
        <nav id="navbar">
          <NavLink to="/" className="nav-button">Home</NavLink>
          <NavLink to="/guitars" className="nav-button">Guitars</NavLink>
          <NavLink to="/models" className="nav-button">Models</NavLink>
          <NavLink to="/info" className="nav-button">Info</NavLink>
          <NavLink to="/login" className="nav-button">Login</NavLink>
        </nav>
      )
}

export default NavBar