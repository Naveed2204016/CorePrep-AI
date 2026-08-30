import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";


const OAuthSuccessPage = () => {

  const navigate = useNavigate();

  const processed = useRef(false);


  useEffect(() => {

    if(processed.current) return;

    processed.current = true;


    const params = new URLSearchParams(
      window.location.search
    );


    const token = params.get("token");
    const id = params.get("id");
    const name = params.get("name");
    const email = params.get("email");


    if(token){

      localStorage.setItem(
        "coreprep_token",
        token
      );


      localStorage.setItem(
        "coreprep_user",
        JSON.stringify({
          id,
          name,
          email
        })
      );


      window.dispatchEvent(
        new Event("coreprep-auth-change")
      );


      navigate("/");

    }
    else{

      navigate("/signin");

    }


  },[navigate]);


  return <div>Logging in with Google...</div>;

};

export default OAuthSuccessPage;
