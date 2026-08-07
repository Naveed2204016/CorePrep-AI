interface GoogleButtonProps {
  onClick: () => void;
}

const GoogleButton = ({ onClick }: GoogleButtonProps) => {
  return (
    <button
      type="button"
      className="google-button"
      onClick={onClick}
    >
      <span className="google-icon">G</span>
      Continue with Google
    </button>
  );
};

export default GoogleButton;