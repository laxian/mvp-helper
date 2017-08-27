package com.etiantian.dywteacher.ui.{page};

import com.etiantian.dywteacher.api.Networks;
import com.etiantian.dywteacher.common.BaseModel;
import com.etiantian.dywteacher.entity.{Bean};
import com.etiantian.dywteacher.entity.Result;
import com.etiantian.dywteacher.global.Constants;
import com.etiantian.dywteacher.mvpframe.rx.RxSchedulerHelper;

import rx.Observable;

/**
 * auto-generate
 * by zwx
 */
public class {alias}Model extends BaseModel implements {alias}Contract.Model {

    @Override
    public Observable<Result<{Bean}>> {apiName}({TypedParams}) {
        return Networks.getInstance().getCommonApi()
                .{apiName}(getParams(Constants.Http.KEY_{API_NAME}
                        {ParamsPair})).compose(RxSchedulerHelper.<Result<{Bean}>>io_main());
    }

}
