import { OnlyHeaderLayout } from "../Layout";
import Check from "../Page/Check";
import Home from "../Page/Home";
import User from "../Page/User";

const publicRoutes = [
  { path: "/", component: Home, layout: OnlyHeaderLayout },
  { path: "/submit", component: User, layout: OnlyHeaderLayout },
  { path: "/check", component: Check, layout: OnlyHeaderLayout },
];
const privateRoutes = [];

export { publicRoutes, privateRoutes };
