import { OnlyHeaderLayout } from "../Layout";
import Home from "../Page/Home";

const publicRoutes = [
  { path: "/", component: Home, layout: OnlyHeaderLayout },
];
const privateRoutes = [];

export { publicRoutes, privateRoutes };