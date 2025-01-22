import App from "./App"
import Specs from "./pages/Specs"
import Login from "./pages/Login"
import Explore from "./pages/Explore"
import Profile from "./pages/Profile"
import Info from "./pages/Info"

const routes = [
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/specs/:serialNumber",
        element: <Specs />
      },
      {
        path: "/login",
        element: <Login />
      },
      {
        path: "/explore",
        element: <Explore />
      },
      {
        path: "/info",
        element: <Info />
      },
      {
        path: "/profile",
        element: <Profile />
      },
    ]
  },
]

export default routes