import os
import sys
from cffi import FFI

ffibuilder = FFI()
ffibuilder.set_source("_soundfile", None)
ffibuilder.cdef("""
enum
{
    SF_FORMAT_SUBMASK       = 0x0000FFFF,
    SF_FORMAT_TYPEMASK      = 0x0FFF0000,
    SF_FORMAT_ENDMASK       = 0x30000000
} ;

enum
{
    SFC_GET_LIB_VERSION             = 0x1000,
    SFC_GET_LOG_INFO                = 0x1001,
    SFC_GET_FORMAT_INFO             = 0x1028,

    SFC_GET_FORMAT_MAJOR_COUNT      = 0x1030,
    SFC_GET_FORMAT_MAJOR            = 0x1031,
    SFC_GET_FORMAT_SUBTYPE_COUNT    = 0x1032,
    SFC_GET_FORMAT_SUBTYPE          = 0x1033,
    SFC_FILE_TRUNCATE               = 0x1080,
    SFC_SET_CLIPPING                = 0x10C0,

    SFC_SET_SCALE_FLOAT_INT_READ    = 0x1014,
    SFC_SET_SCALE_INT_FLOAT_WRITE   = 0x1015,
} ;

enum
{
    SF_FALSE    = 0,
    SF_TRUE     = 1,

    /* Modes for opening files. */
    SFM_READ    = 0x10,
    SFM_WRITE   = 0x20,
    SFM_RDWR    = 0x30,
} ;

typedef int64_t sf_count_t ;

typedef struct SNDFILE_tag SNDFILE ;

typedef struct SF_INFO
{
    sf_count_t frames ;        /* Used to be called samples.  Changed to avoid confusion. */
    int        samplerate ;
    int        channels ;
    int        format ;
    int        sections ;
    int        seekable ;
} SF_INFO ;

SNDFILE*    sf_open          (const char *path, int mode, SF_INFO *sfinfo) ;
int         sf_format_check  (const SF_INFO *info) ;

sf_count_t  sf_seek          (SNDFILE *sndfile, sf_count_t frames, int whence) ;

int         sf_command       (SNDFILE *sndfile, int cmd, void *data, int datasize) ;

int         sf_error         (SNDFILE *sndfile) ;
const char* sf_strerror      (SNDFILE *sndfile) ;
const char* sf_error_number  (int errnum) ;

int         sf_perror        (SNDFILE *sndfile) ;
int         sf_error_str     (SNDFILE *sndfile, char* str, size_t len) ;

int         sf_close         (SNDFILE *sndfile) ;
void        sf_write_sync    (SNDFILE *sndfile) ;

sf_count_t  sf_read_short    (SNDFILE *sndfile, short *ptr, sf_count_t items) ;
sf_count_t  sf_read_int      (SNDFILE *sndfile, int *ptr, sf_count_t items) ;
sf_count_t  sf_read_float    (SNDFILE *sndfile, float *ptr, sf_count_t items) ;
sf_count_t  sf_read_double   (SNDFILE *sndfile, double *ptr, sf_count_t items) ;

/* Note: Data ptr argument types are declared as void* here in order to
         avoid an implicit cast warning. (gh183). */
sf_count_t  sf_readf_short   (SNDFILE *sndfile, void *ptr, sf_count_t frames) ;
sf_count_t  sf_readf_int     (SNDFILE *sndfile, void *ptr, sf_count_t frames) ;
sf_count_t  sf_readf_float   (SNDFILE *sndfile, void *ptr, sf_count_t frames) ;
sf_count_t  sf_readf_double  (SNDFILE *sndfile, void *ptr, sf_count_t frames) ;

sf_count_t  sf_write_short   (SNDFILE *sndfile, short *ptr, sf_count_t items) ;
sf_count_t  sf_write_int     (SNDFILE *sndfile, int *ptr, sf_count_t items) ;
sf_count_t  sf_write_float   (SNDFILE *sndfile, float *ptr, sf_count_t items) ;
sf_count_t  sf_write_double  (SNDFILE *sndfile, double *ptr, sf_count_t items) ;

/* Note: The argument types were changed to void* in order to allow
         writing bytes in SoundFile.buffer_write() */
sf_count_t  sf_writef_short  (SNDFILE *sndfile, void *ptr, sf_count_t frames) ;
sf_count_t  sf_writef_int    (SNDFILE *sndfile, void *ptr, sf_count_t frames) ;
sf_count_t  sf_writef_float  (SNDFILE *sndfile, void *ptr, sf_count_t frames) ;
sf_count_t  sf_writef_double (SNDFILE *sndfile, void *ptr, sf_count_t frames) ;

sf_count_t  sf_read_raw      (SNDFILE *sndfile, void *ptr, sf_count_t bytes) ;
sf_count_t  sf_write_raw     (SNDFILE *sndfile, void *ptr, sf_count_t bytes) ;

const char* sf_get_string    (SNDFILE *sndfile, int str_type) ;
int         sf_set_string    (SNDFILE *sndfile, int str_type, const char* str) ;
const char * sf_version_string (void) ;

typedef sf_count_t  (*sf_vio_get_filelen) (void *user_data) ;
typedef sf_count_t  (*sf_vio_seek)        (sf_count_t offset, int whence, void *user_data) ;
typedef sf_count_t  (*sf_vio_read)        (void *ptr, sf_count_t count, void *user_data) ;
typedef sf_count_t  (*sf_vio_write)       (const void *ptr, sf_count_t count, void *user_data) ;
typedef sf_count_t  (*sf_vio_tell)        (void *user_data) ;

typedef struct SF_VIRTUAL_IO
{    sf_count_t  (*get_filelen) (void *user_data) ;
     sf_count_t  (*seek)        (sf_count_t offset, int whence, void *user_data) ;
     sf_count_t  (*read)        (void *ptr, sf_count_t count, void *user_data) ;
     sf_count_t  (*write)       (const void *ptr, sf_count_t count, void *user_data) ;
     sf_count_t  (*tell)        (void *user_data) ;
} SF_VIRTUAL_IO ;

SNDFILE*    sf_open_virtual   (SF_VIRTUAL_IO *sfvirtual, int mode, SF_INFO *sfinfo, void *user_data) ;
SNDFILE*    sf_open_fd        (int fd, int mode, SF_INFO *sfinfo, int close_desc) ;

typedef struct SF_FORMAT_INFO
{
    int         format ;
    const char* name ;
    const char* extension ;
} SF_FORMAT_INFO ;

enum
{
    // SFC_GET_CUE_COUNT               = 0x10CD,
    // SFC_GET_CUE                     = 0x10CE,
    // SFC_SET_CUE                     = 0x10CF,

    SFC_GET_INSTRUMENT              = 0x10D0,
    SFC_SET_INSTRUMENT              = 0x10D1,

    SFC_GET_LOOP_INFO               = 0x10E0,
};

typedef struct
{   int32_t     indx ;
    uint32_t    position ;
    int32_t     fcc_chunk ;
    int32_t     chunk_start ;
    int32_t     block_start ;
    uint32_t    sample_offset ;
    char name [256] ;
} SF_CUE_POINT ;

typedef struct 
{   uint32_t cue_count ; 
    SF_CUE_POINT cue_points [100] ; 
} SF_CUES;

enum
{   /*
    **  The loop mode field in SF_INSTRUMENT will be one of the following.
    */
    SF_LOOP_NONE = 800,
    SF_LOOP_FORWARD,
    SF_LOOP_BACKWARD,
    SF_LOOP_ALTERNATING
};

typedef struct
{   int gain ;
    char basenote, detune ;
    char velocity_lo, velocity_hi ;
    char key_lo, key_hi ;
    int loop_count ;

    struct
    {   int mode ;
        uint32_t start ;
        uint32_t end ;
        uint32_t count ;
    } loops [16] ; /* make variable in a sensible way */
} SF_INSTRUMENT ;

typedef struct
{
    short   time_sig_num ;  /* any positive integer    > 0  */
    short   time_sig_den ;  /* any positive power of 2 > 0  */
    int     loop_mode ;     /* see SF_LOOP enum             */

    int     num_beats ;     /* this is NOT the amount of quarter notes !!!*/
                            /* a full bar of 4/4 is 4 beats */
                            /* a full bar of 7/8 is 7 beats */

    float   bpm ;           /* suggestion, as it can be calculated using other fields:*/
                            /* file's length, file's sampleRate and our time_sig_den*/
                            /* -> bpms are always the amount of _quarter notes_ per minute */

    int root_key ;          /* MIDI note, or -1 for None */
    int future [6] ;
} SF_LOOP_INFO ;

struct SF_CHUNK_INFO
{   char        id [64] ;   /* The chunk identifier. */
    unsigned    id_size ;   /* The size of the chunk identifier. */
    unsigned    datalen ;   /* The size of that data. */
    void        *data ;     /* Pointer to the data. */
} ;

typedef struct SF_CHUNK_INFO SF_CHUNK_INFO ;

int sf_set_chunk (SNDFILE * sndfile, const SF_CHUNK_INFO * chunk_info) ;
typedef struct SF_CHUNK_ITERATOR SF_CHUNK_ITERATOR ;

SF_CHUNK_ITERATOR *
sf_get_chunk_iterator (SNDFILE * sndfile, const SF_CHUNK_INFO * chunk_info) ;

SF_CHUNK_ITERATOR *
sf_next_chunk_iterator (SF_CHUNK_ITERATOR * iterator) ;

int
sf_get_chunk_size (const SF_CHUNK_ITERATOR * it, SF_CHUNK_INFO * chunk_info) ;

int
sf_get_chunk_data (const SF_CHUNK_ITERATOR * it, SF_CHUNK_INFO * chunk_info) ;
""")

platform = os.environ.get('PYSOUNDFILE_PLATFORM', sys.platform)
if platform == 'win32':
    ffibuilder.cdef("""
    SNDFILE* sf_wchar_open (const wchar_t *wpath, int mode, SF_INFO *sfinfo) ;
    """)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
