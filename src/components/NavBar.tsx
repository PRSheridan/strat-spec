import { NavLink } from "react-router-dom";

function NavBar () {
    return (
        <nav id="navbar">
          <NavLink to="/" className="nav-button">Home</NavLink>
          <NavLink to="/explore" className="nav-button">Explore</NavLink>
          <NavLink to="/info" className="nav-button">Info</NavLink>
          <NavLink to="/login" className="nav-button">Login</NavLink>
        </nav>
      )
}

export default NavBar