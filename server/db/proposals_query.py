# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

import logging

import rethinkdb as r


LOGGER = logging.getLogger(__name__)


async def fetch_proposals_by_target_id(conn, target_id, head_block_num):
    cursor = await r.table('proposals').get_all(
        target_id, index='target_id'
    ).filter(
        (head_block_num >= r.row['start_block_num'])
        & (head_block_num < r.row['end_block_num'])
    ).run(conn)
    proposals = []
    while await cursor.fetch_next():
        proposals.append(await cursor.next())

    return proposals