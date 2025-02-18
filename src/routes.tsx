import App from "./App"
import Login from "./pages/Login"
import List from "./pages/List"
import Specs from "./pages/Specs"
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
        element: <List type='guitars'/>
      },
      {
        path: "/models",
        element: <List type='models'/>
      },
      {
        path: "/guitar/:serialNumber",
        element: <Specs />
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