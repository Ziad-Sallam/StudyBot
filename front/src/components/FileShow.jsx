import { FaFile } from "react-icons/fa";
import { PropTypes } from 'prop-types';
import { GrDocumentPdf } from "react-icons/gr";
import { CiImageOn } from "react-icons/ci";
import { PiFilePptDuotone } from "react-icons/pi";
import { BsFiletypePdf } from "react-icons/bs";
import axios from "axios";

FileShow.propTypes = {
    id: PropTypes.number.isRequired,
    filename: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
};

function FileShow(props) {
    function typeIcon(type) {
        switch (type) {
            case "pdf":
                return <BsFiletypePdf />;
            case "png":
            case "jpeg":
            case "jpg":
                return <CiImageOn />;
            case "pptx":
            case "ppt":
                return <PiFilePptDuotone />;
            default:
                return <FaFile style={{ color: "red" }} />;
        }
    }

    async function getFile() {
        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/get-material-data",
                { id: props.id }
            );
            console.log(response.data);

            const mimeType = {
                'pdf': 'application/pdf',
                'png': 'image/png',
                'jpeg': 'image/jpeg',
                'jpg': 'image/jpeg',
                'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'ppt': 'application/vnd.ms-powerpoint'
            }[props.type] || 'application/octet-stream';

            // Decode base64 to binary
            const byteCharacters = atob(response.data.file_data);
            const byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }
            const byteArray = new Uint8Array(byteNumbers);
            const blob = new Blob([byteArray], { type: mimeType });
            const url = URL.createObjectURL(blob);

            // Open the file URL
            window.open(url);

            // Clean up the URL object after the file is opened
            setTimeout(() => URL.revokeObjectURL(url), 1000);
        } catch (error) {
            console.log(error);
        }
    }

    return (
        <div className="file-show col-lg-2 col-md-4 col-sm-8">
            <div className="data-file">
                {typeIcon(props.type)}
            </div>
            <a className="file-name" onClick={getFile} href="#!">
                {props.filename + "." + props.type}
            </a>
        </div>
    );
}

export default FileShow;
