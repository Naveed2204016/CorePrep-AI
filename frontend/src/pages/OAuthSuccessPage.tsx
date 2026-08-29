import { useEffect } from "react";
import { useNavigate } from "react-router-dom";


const OAuthSuccessPage = () => {

  const navigate = useNavigate();


  useEffect(() => {

    const params = new URLSearchParams(
      window.location.search
    );


    const token = params.get("token");
    const name = params.get("name");
    const email = params.get("email");
    const id = params.get("id");


    if (token) {

      // Store JWT token
      localStorage.setItem(
        "coreprep_token",
        token
      );


      // Store user info for Navbar/Profile
      localStorage.setItem(
        "coreprep_user",
        JSON.stringify({
          id,
          name,
          email,
        })
      );


      // Notify Navbar about login change
      window.dispatchEvent(
        new Event("coreprep-auth-change")
      );


      // Same behavior as normal login
      navigate("/");


    } else {

      navigate("/signin");

    }


  }, [navigate]);


  return (
    <div>
      Logging in with Google...
    </div>
  );
};


export default OAuthSuccessPage;