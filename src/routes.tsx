import App from "./App"
import Specs from "./pages/Specs"
import Login from "./pages/Login"
import Guitars from "./pages/Guitars"
import Models from "./pages/Models"
import Profile from "./pages/Profile"
import Info from "./pages/Info"

const routes = [
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/login",
        element: <Login />
      },
      {
        path: "/guitars",
        element: <Guitars />
      },
      {
        path: "/guitar/:serialNumber",
        element: <Specs />
      },
      {
        path: "/models",
        element: <Models />
      },
      {
        path: "/model/:modelName",
        element: <Specs />
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