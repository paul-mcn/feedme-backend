import fs from "fs";

export const createErrorLogFile = (
  file: fs.PathOrFileDescriptor,
  data: string | Uint8Array
) => {
  fs.appendFile(file, data, (err) => {
    if (err) {
      return console.log(err);
    }
  });
};
