import React, { useState } from "react";
import Spinner from "./Spinner";

function ImageLoader() {
  const [loading, setLoading] = useState(true);

  function handleImageLoad() {
    setLoading(false);
  }

  return (
    <div>
      {loading && <Spinner />}
      <img
        src="path/to/image.jpg"
        alt="Image"
        onLoad={handleImageLoad}
        style={{ display: loading ? "none" : "block" }}
      />
    </div>
  );
}

export default ImageLoader;