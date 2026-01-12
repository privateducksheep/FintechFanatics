import { signOut } from "firebase/auth";
import { auth } from "../lib/firebase";
import { useNavigate } from "react-router-dom";

export default function Wallet() {
  const navigate = useNavigate();
  const user = auth.currentUser;

  const logout = async () => {
    await signOut(auth);
    navigate("/login");
  };

  return (
    <div style={{ padding: 24 }}>
      <h2>Wallet</h2>
      <p>Logged in as: {user?.email}</p>
      <button onClick={logout} style={{ marginTop: 12 }}>
        Log out
      </button>
    </div>
  );
}
